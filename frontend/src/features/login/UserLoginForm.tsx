import { useState } from 'react'
import Logo from '../../assets/logo2.svg?react'

export function UserLoginForm(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const canSubmit = email && password


  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)
    setSuccess(false)

    try {
      const response = await fetch('/api/v1/routers/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          identifier: email,
          password,
          rememberMe: remember
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        setError(data?.detail || 'Login failed.')
        return
      }

        setSuccess(true)
    } catch (err) {
      setError('Something went wrong. Please try again.')
      console.error(err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="relative bg-surface dark:bg-surface px-8 py-10 rounded-2xl shadow-md flex flex-col gap-6 border border-border dark:border-border overflow-hidden"
    >
      <Logo
        className="absolute inset-0 m-auto h-64 w-64 opacity-4 pointer-events-none blur-[1.5px]"
      />
      <div className="relative z-10">
        <h2 className="text-xl font-semibold text-text dark:text-text tracking-wide">
          Log in to your account
        </h2>
        <div className="flex flex-col gap-2">
          <label
            htmlFor="email"
            className="text-sm font-medium text-text-muted dark:text-text-muted"
          >
            Email or Username
          </label>
          <input
            id="email"
            type="text"
            className="w-full rounded-lg px-4 py-2 bg-background-light dark:bg-neutral-800 text-text-dark dark:text-white border border-border focus:outline-none focus:ring-2 focus:ring-accent opacity-90"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label
            htmlFor="password"
            className="text-sm font-medium text-text-muted dark:text-text-muted"
          >
            Password
          </label>
          <input
            id="password"
            type="password"
            className="w-full rounded-lg px-4 py-2 bg-background-light dark:bg-neutral-800 text-text-dark dark:text-white border border-border focus:outline-none focus:ring-2 focus:ring-accent opacity-90"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-text-muted dark:text-text-muted">
            <input
              type="checkbox"
              className="accent-accent"
              checked={remember}
              onChange={(e) => setRemember(e.target.checked)}
            />
            Remember me
          </label>
        </div>
        <button
          type="submit"
          className="mt-2 w-full flex items-center justify-center bg-accent text-black font-medium py-2 px-4 rounded-xl hover:bg-accent-muted transition disabled:opacity-50"
          disabled={isSubmitting || !canSubmit}
        >Login</button>
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}
      {success && (
        <p className="text-sm text-green-500">Login successful!</p>
        // TODO: Handle token parsing and storage, then redirect.
      )}

    </form>
  )
}