type HeadingProps = {
  children: React.ReactNode
}

export function Heading({ children }: HeadingProps) {
  return (
    <h1 className="text-3xl font-bold text-shadowmint dark:text-cryoCore">
      {children}
    </h1>
  )
}
