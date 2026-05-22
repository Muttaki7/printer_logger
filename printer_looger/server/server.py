import os
import uuid
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["printer_project"]
jobs = db["jobs"]
printers = db["printers"]  # optional, but we'll seed some for printer selection

# API Key authentication
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set in environment variables")


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get("X-API-Key")
        if not provided_key or provided_key != API_KEY:
            abort(401, description="Invalid or missing API key")
        return f(*args, **kwargs)

    return decorated


# ---- Helpers ----
def serialize_doc(doc):
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id"))
    for key in list(doc.keys()):
        if isinstance(doc[key], datetime):
            doc[key] = doc[key].strftime("%Y-%m-%d %H:%M:%S")
    return doc


def generate_print_id():
    today = datetime.now().strftime("%Y%m%d")
    short_id = str(uuid.uuid4())[:6].upper()
    return f"PRINT-{today}-{short_id}"


def get_default_printer(department):
    """Return a printer model for the department (simple round‑robin or first)."""
    printer = printers.find_one({"department": department, "is_active": True})
    if not printer:
        return {"model_number": "Default Printer", "ip_address": "0.0.0.0"}
    return printer


# ---- Seed data (only once) ----
def seed_printers():
    if printers.count_documents({}) == 0:
        default_printers = [
            {
                "printer_name": "Knitting_Printer_1",
                "department": "Knitting",
                "model_number": "RICOH MP 3555",
                "ip_address": "192.168.1.101",
                "is_active": True,
            },
            {
                "printer_name": "Legal_Printer_1",
                "department": "Legal",
                "model_number": "HP LaserJet M455",
                "ip_address": "192.168.1.110",
                "is_active": True,
            },
            {
                "printer_name": "IT_Printer_1",
                "department": "IT",
                "model_number": "RICOH IM C4500",
                "ip_address": "192.168.1.120",
                "is_active": True,
            },
            {
                "printer_name": "Mechanic_Printer_1",
                "department": "Mechanic",
                "model_number": "Brother HL-L6200",
                "ip_address": "192.168.1.130",
                "is_active": True,
            },
            {
                "printer_name": "Technician_Printer_1",
                "department": "Technician",
                "model_number": "Xerox VersaLink C405",
                "ip_address": "192.168.1.140",
                "is_active": True,
            },
        ]
        printers.insert_many(default_printers)


# Run setup
seed_printers()
jobs.create_index([("print_id", ASCENDING)], unique=True)
jobs.create_index([("status", ASCENDING), ("created_at", DESCENDING)])


# ---- Routes ----
@app.route("/")
def index():
    return jsonify({"message": "Print Automation API", "status": "running"})


@app.route("/api/jobs", methods=["GET"])
@require_api_key
def get_jobs():
    department = request.args.get("department")
    status = request.args.get("status", "pending")
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))

    query = {"status": status}
    if department and department != "All":
        query["department"] = department

    total = jobs.count_documents(query)
    cursor = jobs.find(query).sort("created_at", DESCENDING).skip(offset).limit(limit)
    job_list = [serialize_doc(doc) for doc in cursor]

    return jsonify({"jobs": job_list, "total": total, "limit": limit, "offset": offset})


@app.route("/api/jobs", methods=["POST"])
@require_api_key
def create_job():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["user_id", "file_name", "page_amount", "department"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    try:
        page_amount = int(data["page_amount"])
        copies = int(data.get("copies", 1))
    except ValueError:
        return jsonify({"error": "page_amount and copies must be integers"}), 400

    printer = get_default_printer(data["department"])
    print_id = generate_print_id()

    job_doc = {
        "print_id": print_id,
        "user_id": data["user_id"],
        "file_name": data["file_name"],
        "page_amount": page_amount,
        "copies": copies,
        "department": data["department"],
        "printer_model_number": printer["model_number"],
        "status": "pending",
        "created_at": datetime.utcnow(),
        "print_start_time": None,
    }
    result = jobs.insert_one(job_doc)

    return (
        jsonify(
            {
                "message": "Job created successfully",
                "job_id": str(result.inserted_id),
                "print_id": print_id,
                "assigned_printer": printer["model_number"],
            }
        ),
        201,
    )


@app.route("/api/jobs/<job_id>/print", methods=["PUT"])
@require_api_key
def print_job(job_id):
    try:
        oid = ObjectId(job_id)
    except:
        return jsonify({"error": "Invalid job ID"}), 400

    job = jobs.find_one({"_id": oid, "status": "pending"})
    if not job:
        return jsonify({"error": "Job not found or already printed/deleted"}), 404

    now = datetime.utcnow()
    jobs.update_one(
        {"_id": oid}, {"$set": {"status": "printed", "print_start_time": now}}
    )

    # Simulate sending to printer
    print(
        f"[SIMULATION] Sending {job['print_id']} to printer {job.get('printer_model_number')}"
    )

    return jsonify(
        {
            "message": f"Job {job['print_id']} printed successfully",
            "print_start_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@app.route("/api/jobs/<job_id>", methods=["DELETE"])
@require_api_key
def delete_job(job_id):
    try:
        oid = ObjectId(job_id)
    except:
        return jsonify({"error": "Invalid job ID"}), 400

    result = jobs.update_one({"_id": oid}, {"$set": {"status": "deleted"}})
    if result.matched_count == 0:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({"message": "Job deleted successfully"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
