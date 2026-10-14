import React, { useState, useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AuthContext } from '../App'
import { auth } from '../services/api'

export default function Register() {
  const [form, setForm] = useState({ fullName: '', email: '', password: '', confirmPassword: '', monthlyIncome: '', currency: 'INR', financialGoal: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useContext(AuthContext)
  const navigate = useNavigate()

  const update = (field, value) => setForm({ ...form, [field]: value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match')
      return
    }
    if (form.password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }
    setLoading(true)
    try {
      const data = await auth.register({
        fullName: form.fullName,
        email: form.email,
        password: form.password,
        confirmPassword: form.confirmPassword,
        monthlyIncome: form.monthlyIncome ? Number(form.monthlyIncome) : 0,
        currency: form.currency,
        financialGoal: form.financialGoal,
      })
      login(data.token, data.user)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p>Start your journey to financial freedom with FinWise AI</p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input type="text" value={form.fullName} onChange={e => update('fullName', e.target.value)} required placeholder="John Doe" />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={form.email} onChange={e => update('email', e.target.value)} required placeholder="you@example.com" />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Password</label>
              <input type="password" value={form.password} onChange={e => update('password', e.target.value)} required placeholder="Min 6 characters" />
            </div>
            <div className="form-group">
              <label>Confirm Password</label>
              <input type="password" value={form.confirmPassword} onChange={e => update('confirmPassword', e.target.value)} required placeholder="Repeat password" />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Monthly Income</label>
              <input type="number" value={form.monthlyIncome} onChange={e => update('monthlyIncome', e.target.value)} placeholder="e.g. 50000" />
            </div>
            <div className="form-group">
              <label>Currency</label>
              <select value={form.currency} onChange={e => update('currency', e.target.value)}>
                <option value="INR">INR (₹)</option>
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </select>
            </div>
          </div>
          <div className="form-group">
            <label>Financial Goal</label>
            <input type="text" value={form.financialGoal} onChange={e => update('financialGoal', e.target.value)} placeholder="e.g. Save for a car" />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>
        <div className="link">
          Already have an account? <Link to="/login">Sign In</Link>
        </div>
      </div>
    </div>
  )
}
