import React from 'react'
import { AlertCircle } from 'lucide-react'
import { Button } from './ui/Button'

interface Props {
  children: React.ReactNode
  fallback?: React.ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('[ErrorBoundary] caught:', error, info)
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="flex flex-col items-center justify-center gap-4 py-16 px-6 text-center min-h-[40vh]">
          <div className="w-14 h-14 rounded-full bg-rust/20 flex items-center justify-center">
            <AlertCircle className="w-7 h-7 text-rust" />
          </div>
          <div>
            <h2 className="font-serif text-2xl text-cream mb-2">Something went wrong</h2>
            <p className="text-stone-light font-sans text-sm max-w-xs">
              {this.state.error?.message ?? 'An unexpected error occurred.'}
            </p>
          </div>
          <Button
            variant="ghost"
            onClick={() => window.location.reload()}
          >
            Reload page
          </Button>
          {this.state.error?.message !== 'An unexpected error occurred.' && (
            <button
              onClick={this.handleReset}
              className="text-stone-light text-xs underline-offset-2 hover:text-cream transition-colors"
            >
              Try without reloading
            </button>
          )}
        </div>
      )
    }

    return this.props.children
  }
}
