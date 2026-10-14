import React, { useState, useEffect } from 'react'
import { savings } from '../services/api'
import { Plus, Edit2, Trash2, X, Target, TrendingUp } from 'lucide-react'

export default function Savings() {
  const [goals, setGoals] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [showDepositModal, setShowDepositModal] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [depositItem, setDepositItem] = useState(null)
  const [depositAmount, setDepositAmount] = useState('')
  const [form, setForm] = useState({ name: '', target_amount: '', current_amount: '', deadline: '', description: '' })
  const [saving, setSaving] = useState(false)

  const fetchGoals = async () => {
    setLoading(true)
    try {
      const data = await savings.getAll()
      setGoals(data.savings || data.goals || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchGoals() }, [])

  const openAdd = () => { setEditItem(null); setForm({ name: '', target_amount: '', current_amount: '0', deadline: '', description: '' }); setShowModal(true) }
  const openEdit = (g) => { setEditItem(g); setForm({ name: g.name, target_amount: String(g.target_amount), current_amount: String(g.current_amount || 0), deadline: g.deadline ? g.deadline.split('T')[0] : '', description: g.description || '' }); setShowModal(true) }
  const openDeposit = (g) => { setDepositItem(g); setDepositAmount(''); setShowDepositModal(true) }

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const payload = { ...form, target_amount: parseFloat(form.target_amount), current_amount: parseFloat(form.current_amount || 0) }
      if (editItem) {
        await savings.update(editItem.id || editItem._id, payload)
      } else {
        await savings.create(payload)
      }
      setShowModal(false)
      fetchGoals()
    } catch (err) {
      alert(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDeposit = async (e) => {
    e.preventDefault()
    const amt = parseFloat(depositAmount)
    if (isNaN(amt) || amt <= 0) return alert('Enter a valid amount')
    try {
      const newAmount = (depositItem.current_amount || 0) + amt
      await savings.update(depositItem.id || depositItem._id, { current_amount: newAmount })
      setShowDepositModal(false)
      fetchGoals()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this savings goal?')) return
    try {
      await savings.delete(id)
      fetchGoals()
    } catch (err) {
      alert(err.message)
    }
  }

  const fmt = (n) => `$${Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}`

  const totalSaved = goals.reduce((s, g) => s + (g.current_amount || 0), 0)
  const totalTarget = goals.reduce((s, g) => s + (g.target_amount || 0), 0)

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Savings Goals</h2>
          <p>Track progress toward your financial goals</p>
        </div>
        <button className="btn btn-primary" onClick={openAdd}><Plus size={16} /> Add Goal</button>
      </div>

      <div className="stat-cards" style={{ marginBottom: 24 }}>
        <div className="stat-card savings">
          <div className="label"><Target size={16} /> Total Saved</div>
          <div className="value" style={{ color: 'var(--secondary)' }}>{fmt(totalSaved)}</div>
        </div>
        <div className="stat-card balance">
          <div className="label"><TrendingUp size={16} /> Total Target</div>
          <div className="value" style={{ color: 'var(--primary)' }}>{fmt(totalTarget)}</div>
        </div>
        <div className="stat-card income">
          <div className="label">Overall Progress</div>
          <div className="value" style={{ color: 'var(--success)' }}>{totalTarget > 0 ? ((totalSaved / totalTarget) * 100).toFixed(1) : 0}%</div>
        </div>
      </div>

      {loading ? <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>Loading...</div> : goals.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: 60 }}>
          <Target size={48} style={{ color: 'var(--text-muted)', marginBottom: 16 }} />
          <h3 style={{ marginBottom: 8 }}>No Savings Goals</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 20 }}>Create your first savings goal to start building wealth</p>
          <button className="btn btn-primary" onClick={openAdd}>Create Goal</button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 16 }}>
          {goals.map(g => {
            const pct = Math.min(((g.current_amount || 0) / g.target_amount) * 100, 100)
            const reached = (g.current_amount || 0) >= g.target_amount
            return (
              <div key={g.id || g._id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                  <div>
                    <h3 style={{ fontSize: 16, fontWeight: 600 }}>{g.name}</h3>
                    {g.description && <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>{g.description}</p>}
                  </div>
                  <div style={{ display: 'flex', gap: 4 }}>
                    <button className="btn btn-ghost btn-sm" onClick={() => openEdit(g)}><Edit2 size={14} /></button>
                    <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(g.id || g._id)} style={{ color: 'var(--danger)' }}><Trash2 size={14} /></button>
                  </div>
                </div>
                {g.deadline && <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 8 }}>Target: {new Date(g.deadline).toLocaleDateString()}</div>}
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Saved: {fmt(g.current_amount)}</span>
                  <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Goal: {fmt(g.target_amount)}</span>
                </div>
                <div className="progress-bar">
                  <div className={`fill ${reached ? 'ok' : pct >= 80 ? 'warning' : 'ok'}`} style={{ width: `${pct}%` }} />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{pct.toFixed(0)}% complete</span>
                  {!reached && <button className="btn btn-success btn-sm" onClick={() => openDeposit(g)}>Add Funds</button>}
                  {reached && <span className="tag tag-positive">Goal Reached!</span>}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h3>{editItem ? 'Edit Goal' : 'Add Savings Goal'}</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setShowModal(false)}><X size={18} /></button>
            </div>
            <form onSubmit={handleSave}>
              <div className="form-group">
                <label>Goal Name</label>
                <input type="text" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required placeholder="e.g., Emergency Fund" />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Target Amount</label>
                  <input type="number" step="0.01" min="1" value={form.target_amount} onChange={e => setForm({...form, target_amount: e.target.value})} required placeholder="0.00" />
                </div>
                <div className="form-group">
                  <label>Already Saved</label>
                  <input type="number" step="0.01" min="0" value={form.current_amount} onChange={e => setForm({...form, current_amount: e.target.value})} placeholder="0.00" />
                </div>
              </div>
              <div className="form-group">
                <label>Target Date (optional)</label>
                <input type="date" value={form.deadline} onChange={e => setForm({...form, deadline: e.target.value})} />
              </div>
              <div className="form-group">
                <label>Description (optional)</label>
                <textarea value={form.description} onChange={e => setForm({...form, description: e.target.value})} rows={2} placeholder="Why is this goal important?" />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Saving...' : (editItem ? 'Update' : 'Create')}</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showDepositModal && depositItem && (
        <div className="modal-overlay" onClick={() => setShowDepositModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h3>Add Funds to "{depositItem.name}"</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setShowDepositModal(false)}><X size={18} /></button>
            </div>
            <form onSubmit={handleDeposit}>
              <div className="form-group">
                <label>Deposit Amount</label>
                <input type="number" step="0.01" min="0.01" value={depositAmount} onChange={e => setDepositAmount(e.target.value)} required placeholder="0.00" autoFocus />
              </div>
              <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 16 }}>
                Current: {fmt(depositItem.current_amount)} / Target: {fmt(depositItem.target_amount)}
              </p>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowDepositModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-success">Deposit</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
