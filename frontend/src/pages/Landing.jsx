import React from 'react'
import { Link } from 'react-router-dom'
import { BarChart3, Brain, Shield, TrendingUp, Wallet, Target, LineChart, Bell } from 'lucide-react'

const features = [
  { icon: <BarChart3 size={24} />, color: '#6366f1', title: 'Smart Dashboard', desc: 'Get a real-time overview of your finances with beautiful charts and insights.' },
  { icon: <Brain size={24} />, color: '#06b6d4', title: 'AI Advisor', desc: 'Chat with an AI-powered advisor that analyzes your spending and gives personalized advice.' },
  { icon: <Target size={24} />, color: '#10b981', title: 'Budget Management', desc: 'Set monthly budgets and track your spending against each category.' },
  { icon: <TrendingUp size={24} />, color: '#f59e0b', title: 'Savings Goals', desc: 'Create and track savings goals with progress visualization.' },
  { icon: <LineChart size={24} />, color: '#ec4899', title: 'Detailed Reports', desc: 'Generate monthly and yearly reports with downloadable summaries.' },
  { icon: <Bell size={24} />, color: '#ef4444', title: 'Smart Alerts', desc: 'Get notified about budget overruns, unusual spending, and goal milestones.' },
]

const steps = [
  { num: '1', title: 'Create Account', desc: 'Sign up in seconds with your email.' },
  { num: '2', title: 'Add Transactions', desc: 'Log your income and expenses easily.' },
  { num: '3', title: 'Get AI Insights', desc: 'Let our AI analyze and optimize your finances.' },
]

export default function Landing() {
  return (
    <div>
      <nav className="landing-nav">
        <div className="logo">FinWise AI</div>
        <div className="links">
          <Link to="/login" className="btn btn-ghost">Login</Link>
          <Link to="/register" className="btn btn-primary">Get Started</Link>
        </div>
      </nav>

      <section className="hero">
        <div>
          <h1>Take Control of Your <span className="gradient">Financial Future</span></h1>
          <p>FinWise AI combines powerful tracking tools with artificial intelligence to help you make smarter financial decisions, save more, and achieve your goals faster.</p>
          <div className="hero-buttons">
            <Link to="/register" className="btn btn-primary">Start Free Trial</Link>
            <Link to="/login" className="btn btn-secondary">Sign In</Link>
          </div>
        </div>
      </section>

      <section className="landing-section">
        <h2>Powerful Features</h2>
        <p className="subtitle">Everything you need to master your personal finances</p>
        <div className="features-grid">
          {features.map((f, i) => (
            <div key={i} className="feature-card">
              <div className="icon" style={{ background: `${f.color}20`, color: f.color }}>{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="landing-section">
        <h2>How It Works</h2>
        <p className="subtitle">Get started in three simple steps</p>
        <div className="features-grid">
          {steps.map((s, i) => (
            <div key={i} className="feature-card" style={{ textAlign: 'center' }}>
              <div className="icon" style={{ background: 'var(--primary)', color: 'white', margin: '0 auto 16px', fontSize: '20px', fontWeight: 700 }}>{s.num}</div>
              <h3>{s.title}</h3>
              <p>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="landing-section" style={{ textAlign: 'center' }}>
        <h2>Ready to Start?</h2>
        <p className="subtitle">Join thousands of users who are already improving their finances</p>
        <Link to="/register" className="btn btn-primary" style={{ fontSize: 16, padding: '14px 32px' }}>Create Free Account</Link>
      </section>

      <footer style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)', borderTop: '1px solid var(--border)', fontSize: 14 }}>
        &copy; 2026 FinWise AI. All rights reserved.
      </footer>
    </div>
  )
}
