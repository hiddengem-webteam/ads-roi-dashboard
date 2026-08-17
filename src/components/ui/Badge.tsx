import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'neutral';
  children: ReactNode;
  className?: string;
}

const variants = {
  default: 'bg-[var(--fill-blue)] text-[var(--brand)]',
  neutral: 'bg-[var(--fill-gray)] text-[var(--muted)]',
  success: 'bg-[rgba(48,209,88,.12)] text-[var(--success-ink)]',
  warning: 'bg-[rgba(255,159,10,.12)] text-[var(--warning-ink)]',
  error: 'bg-[rgba(220,38,38,.1)] text-[var(--danger)]',
  info: 'bg-[var(--fill-blue)] text-[var(--brand)]',
};

export function Badge({ variant = 'default', children, className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold',
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
