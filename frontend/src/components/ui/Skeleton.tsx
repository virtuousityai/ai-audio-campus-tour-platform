interface SkeletonProps {
  className?: string
  count?: number
}

function SkeletonItem({ className = '' }: { className?: string }) {
  return (
    <div
      className={`animate-pulse bg-white/10 rounded-lg ${className}`}
      aria-hidden="true"
    />
  )
}

export function Skeleton({ className = '', count = 1 }: SkeletonProps) {
  if (count === 1) {
    return <SkeletonItem className={className} />
  }

  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonItem key={i} className={className} />
      ))}
    </>
  )
}
