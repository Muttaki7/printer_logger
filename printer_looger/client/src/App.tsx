import { useState, useEffect, useCallback } from 'react'
import './App.css'

const API_BASE = ''  // proxied via vite, empty base avoids double /api
const API_KEY = import.meta.env.VITE_API_KEY  // set in .env.local

const DEPARTMENTS = ['Knitting', 'Legal', 'IT', 'Mechanic', 'Technician']

interface Job {
  id: string
  print_id: string
  user_id: string
  file_name: string
  page_amount: number
  copies: number
  department: string
  printer_model_number: string
  status: string
  created_at: string
  print_start_time: string | null
}

const emptyForm = {
  user_id: '',
  file_name: '',
  page_amount: '',
  copies: '1',
  department: DEPARTMENTS[0],
}

function App() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [total, setTotal] = useState(0)
  const [statusFilter, setStatusFilter] = useState('pending')
  const [deptFilter, setDeptFilter] = useState('All')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState(emptyForm)
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')
  const [formSuccess, setFormSuccess] = useState('')
  const [actionLoading, setActionLoading] = useState<string | null>(null)

  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY || '',
  }

  const fetchJobs = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams({ status: statusFilter, limit: '20' })
      if (deptFilter !== 'All') params.set('department', deptFilter)
      const res = await fetch(`${API_BASE}/api/jobs?${params}`, { headers })
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      const data = await res.json()
      setJobs(data.jobs)
      setTotal(data.total)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load jobs')
    } finally {
      setLoading(false)
    }
  }, [statusFilter, deptFilter])

  useEffect(() => {
    // Schedule fetchJobs asynchronously to avoid triggering synchronous setState in the effect
    const t = setTimeout(() => {
      fetchJobs()
    }, 0)
    return () => clearTimeout(t)
  }, [fetchJobs])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setFormError('')
    setFormSuccess('')
    setSubmitting(true)
    try {
      const res = await fetch(`${API_BASE}/api/jobs`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          ...form,
          page_amount: parseInt(form.page_amount, 10),
          copies: parseInt(form.copies, 10),
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed to create job')
      setFormSuccess(`Created: ${data.print_id} → ${data.assigned_printer}`)
      setForm(emptyForm)
      fetchJobs()
    } catch (e: unknown) {
      setFormError(e instanceof Error ? e.message : 'Request failed')
    } finally {
      setSubmitting(false)
    }
  }

  async function handlePrint(job: Job) {
    setActionLoading(job.id)
    try {
      const res = await fetch(`${API_BASE}/api/jobs/${job.id}/print`, { method: 'PUT', headers })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed to print')
      fetchJobs()
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : 'Action failed')
    } finally {
      setActionLoading(null)
    }
  }

  async function handleDelete(job: Job) {
    if (!confirm(`Delete job ${job.print_id}?`)) return
    setActionLoading(job.id)
    try {
      const res = await fetch(`${API_BASE}/api/jobs/${job.id}`, { method: 'DELETE', headers })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed to delete')
      fetchJobs()
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : 'Action failed')
    } finally {
      setActionLoading(null)
    }
  }

  return (
    <div className="layout">
      <header className="header">
        <h1>📄 Print Job Dashboard</h1>
        <span className="header-sub">MongoDB · {total} jobs</span>
      </header>

      <main className="main">
        <aside className="sidebar">
          <h2>New Print Job</h2>
          <form className="form" onSubmit={handleSubmit}>
            <label>User ID <input required value={form.user_id} onChange={e => setForm(f => ({ ...f, user_id: e.target.value }))} placeholder="e.g. john.doe" /></label>
            <label>File Name <input required value={form.file_name} onChange={e => setForm(f => ({ ...f, file_name: e.target.value }))} placeholder="e.g. report.pdf" /></label>
            <label>Department <select value={form.department} onChange={e => setForm(f => ({ ...f, department: e.target.value }))}>{DEPARTMENTS.map(d => <option key={d}>{d}</option>)}</select></label>
            <label>Pages <input required type="number" min="1" value={form.page_amount} onChange={e => setForm(f => ({ ...f, page_amount: e.target.value }))} /></label>
            <label>Copies <input required type="number" min="1" value={form.copies} onChange={e => setForm(f => ({ ...f, copies: e.target.value }))} /></label>
            {formError && <p className="msg error">{formError}</p>}
            {formSuccess && <p className="msg success">{formSuccess}</p>}
            <button type="submit" disabled={submitting}>{submitting ? 'Submitting…' : 'Create Job'}</button>
          </form>
        </aside>

        <section className="content">
          <div className="filters">
            <div className="tabs">
              {['pending', 'printed', 'deleted'].map(s => (
                <button key={s} className={`tab ${statusFilter === s ? 'active' : ''}`} onClick={() => setStatusFilter(s)}>
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </button>
              ))}
            </div>
            <select className="dept-select" value={deptFilter} onChange={e => setDeptFilter(e.target.value)}>
              <option value="All">All Departments</option>
              {DEPARTMENTS.map(d => <option key={d}>{d}</option>)}
            </select>
            <button className="refresh-btn" onClick={fetchJobs} disabled={loading}>{loading ? '…' : '↻ Refresh'}</button>
          </div>

          {error && <p className="msg error">{error}</p>}
          {loading && <p className="loading">Loading jobs…</p>}

          {!loading && jobs.length === 0 && (
            <p className="empty">No {statusFilter} jobs{deptFilter !== 'All' ? ` in ${deptFilter}` : ''}.</p>
          )}

          <div className="job-list">
            {jobs.map(job => (
              <div key={job.id} className={`job-card status-${job.status}`}>
                <div className="job-header">
                  <span className="print-id">{job.print_id}</span>
                  <span className={`badge ${job.status}`}>{job.status}</span>
                </div>
                <div className="job-body">
                  <div><span>User</span>{job.user_id}</div>
                  <div><span>File</span>{job.file_name}</div>
                  <div><span>Dept</span>{job.department}</div>
                  <div><span>Pages</span>{job.page_amount} × {job.copies}</div>
                  <div><span>Printer</span>{job.printer_model_number}</div>
                  <div><span>Created</span>{job.created_at}</div>
                  {job.print_start_time && <div><span>Printed</span>{job.print_start_time}</div>}
                </div>
                {job.status === 'pending' && (
                  <div className="job-actions">
                    <button className="btn-print" disabled={actionLoading === job.id} onClick={() => handlePrint(job)}>
                      {actionLoading === job.id ? '…' : '🖨️ Print'}
                    </button>
                    <button className="btn-delete" disabled={actionLoading === job.id} onClick={() => handleDelete(job)}>
                      🗑️ Delete
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App