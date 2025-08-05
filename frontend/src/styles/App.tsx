import { useRoutes } from 'react-router-dom'
import routes from '../routes'
import { Heading } from '../components/Heading.tsx'
import { ThemeToggle } from '../components/ThemeToggle.tsx'

function App() {
  const element = useRoutes(routes)
  console.log('Resolved element:', element)

  return (
    <div className="min-h-screen bg-white text-black dark:bg-neutral-900 dark:text-white transition-colors duration-300">
      <header className="p-4 border-b border-gray-200 dark:border-gray-700">
        <ThemeToggle />
      </header>
      <main className="p-4 flex flex-col items-center justify-center space-y-4">

        <Heading>Welcome to Project Nox</Heading>
        <p>This is the future home of your platform.</p>
        {element}
      </main>
    </div>
  )
}

export default App
