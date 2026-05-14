interface BadgeProps {
  label: string
  emoji?: string
  active?: boolean
  onClick?: () => void
}

export function Badge({ label, emoji, active = false, onClick }: BadgeProps) {
  const base =
    'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-sans font-medium transition-colors duration-150'

  const activeStyle = 'bg-gold text-white'
  const inactiveStyle = 'bg-parchment/20 text-stone-light border border-stone-light/30'

  return (
    <span
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onClick={onClick}
      onKeyDown={onClick ? (e) => e.key === 'Enter' && onClick() : undefined}
      className={`${base} ${active ? activeStyle : inactiveStyle} ${onClick ? 'cursor-pointer hover:opacity-80 select-none' : ''}`}
    >
      {emoji && <span aria-hidden="true">{emoji}</span>}
      {label}
    </span>
  )
}
