import { useState } from 'react'
import { Loader } from '../../components/Loader.tsx'

export function RegistrationForm() {
  const [email, setEmail] = useState('')
  const [userName, setUsername] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [password, setPassword] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          user_name: userName,
          display_name: displayName,
          password,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        setError(data?.detail || 'Registration failed.')
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
      className="w-full max-w-xl bg-surface dark:bg-surface px-8 py-10 rounded-2xl shadow-md flex flex-col gap-6 border border-border dark:border-border"
    >
      <h2 className="text-xl font-semibold text-text dark:text-text tracking-wide">
        Create your account
      </h2>

      <div className="flex flex-col gap-2">
        <label
          htmlFor="email"
          className="text-sm font-medium text-text-muted dark:text-text-muted"
        >
          Email
        </label>
        <input
          id="email"
          type="email"
          className="w-full rounded-lg px-4 py-2 bg-background-light dark:bg-neutral-800 text-text-dark dark:text-white border border-border focus:outline-none focus:ring-2 focus:ring-accent"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="flex flex-col gap-2">
        <label
          htmlFor="username"
          className="text-sm font-medium text-text-muted dark:text-text-muted"
        >
          Username
        </label>
        <input
          id="username"
          type="text"
          className="w-full rounded-lg px-4 py-2 bg-background-light dark:bg-neutral-800 text-text-dark dark:text-white border border-border focus:outline-none focus:ring-2 focus:ring-accent"
          value={userName}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div className="flex flex-col gap-2">
        <label
          htmlFor="displayName"
          className="text-sm font-medium text-text-muted dark:text-text-muted"
        >
          Display Name
        </label>
        <input
          id="displayName"
          type="text"
          className="w-full rounded-lg px-4 py-2 bg-background-light dark:bg-neutral-800 text-text-dark dark:text-white border border-border focus:outline-none focus:ring-2 focus:ring-accent"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
        />
      </div>

      <div className="flex flex-col gap-2">
        <label
          htmlFor="password"
          className="text-sm font-medium text-text-muted dark:text-text-muted"
        >
          Password
        </label>
        <input
          id="password"
          type="password"
          className="w-full rounded-lg px-4 py-2 bg-background-light dark:bg-neutral-800 text-text-dark dark:text-white border border-border focus:outline-none focus:ring-2 focus:ring-accent"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}
      {success && (
        <p className="text-sm text-green-500">Registration successful!</p>
      )}

      <button
        type="submit"
        className="mt-2 w-full flex items-center justify-center bg-accent text-black font-medium py-2 px-4 rounded-xl hover:bg-accent-muted transition disabled:opacity-50"
        disabled={isSubmitting}
      >
        {isSubmitting ? <Loader /> : 'Register'}
      </button>
    </form>
  )
}
