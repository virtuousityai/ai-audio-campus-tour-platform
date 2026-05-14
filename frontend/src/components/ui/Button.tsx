import React from 'react'

type ButtonVariant = 'primary' | 'ghost' | 'icon'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  isLoading?: boolean
  children: React.ReactNode
}

export function Button({
  variant = 'primary',
  isLoading = false,
  disabled,
  children,
  className = '',
  ...props
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center font-sans font-medium transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-gold select-none'

  const variants: Record<ButtonVariant, string> = {
    primary:
      'bg-gold text-white px-6 py-3 rounded-lg hover:bg-gold-light active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed text-sm tracking-wide',
    ghost:
      'border border-gold text-gold px-5 py-2.5 rounded-lg hover:bg-gold/10 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed text-sm',
    icon: 'w-10 h-10 rounded-full hover:bg-white/10 active:scale-90 disabled:opacity-40 disabled:cursor-not-allowed',
  }

  return (
    <button
      disabled={disabled || isLoading}
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center gap-2">
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
          Loading…
        </span>
      ) : (
        children
      )}
    </button>
  )
}
