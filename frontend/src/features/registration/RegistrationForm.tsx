import { useState } from 'react'
import { Loader } from '../../components/Loader.tsx'

export function RegistrationForm() {
  const [email, setEmail] = useState('')
  const [userName, setUsername] = useState('')
  const [displayname, setDisplayname] = useState('')
  const [password, setPassword] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const inputClass =
    'flex-1 rounded border border-gray-300 px-3 py-2 ' +
    'bg-white text-black dark:bg-neutral-800 dark:text-white ' +
    'focus:outline-none focus:ring-2 focus:ring-shadowmint'

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const response = await fetch(
        'http://localhost:8000/api/v1/auth/register',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email,
            username: userName,
            display_name: displayname,
            password,
          }),
        }
      )

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
      className="flex flex-col gap-6 w-full max-w-md mt-8"
      onSubmit={handleSubmit}
    >
      <div className="flex items-center gap-4">
        <label htmlFor="email" className="w-28 shrink-0">
          Email
        </label>
        <input
          id="email"
          type="email"
          className={inputClass}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="flex items-center gap-4">
        <label htmlFor="userName" className="w-28 shrink-0">
          Username
        </label>
        <input
          id="userName"
          type="text"
          className={inputClass}
          value={userName}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="flex items-center gap-4">
        <label htmlFor="displayname" className="w-28 shrink-0">
          Display Name
        </label>
        <input
          id="displayname"
          type="text"
          className={inputClass}
          value={displayname}
          onChange={(e) => setDisplayname(e.target.value)}
        />
      </div>
      <div className="flex items-center gap-4">
        <label htmlFor="password" className="w-28 shrink-0">
          Password
        </label>
        <input
          id="password"
          type="password"
          className={inputClass}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      {error && <p className="text-red-500">{error}</p>}
      {success && <p className="text-green-500">Registration successful!</p>}
      <button
        type="submit"
        className="flex items-center justify-center w-full"
        disabled={isSubmitting}
      >
        {isSubmitting ? <Loader /> : 'Submit'}
      </button>
    </form>
  )
}
