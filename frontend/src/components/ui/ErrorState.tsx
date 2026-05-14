import { AlertCircle } from 'lucide-react'
import { Button } from './Button'

interface ErrorStateProps {
  message: string
  onRetry?: () => void
}

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12 px-6 text-center">
      <div className="w-12 h-12 rounded-full bg-rust/20 flex items-center justify-center">
        <AlertCircle className="w-6 h-6 text-rust" />
      </div>
      <div>
        <p className="text-stone-light font-sans text-sm leading-relaxed max-w-xs">{message}</p>
      </div>
      {onRetry && (
        <Button variant="ghost" onClick={onRetry}>
          Try again
        </Button>
      )}
    </div>
  )
}
