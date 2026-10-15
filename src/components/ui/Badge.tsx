import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'neutral';
  children: ReactNode;
  className?: string;
  /** Hide the status dot (for purely descriptive tags). */
  noDot?: boolean;
}

// Same shape as the weekly reports' .badge: hairline border, tinted fill,
// 8px status dot, 12px/500 Inter.
const variants = {
  default: { pill: 'bg-[var(--brand-bg)] text-[var(--brand-text)] border-[var(--brand-border)]', dot: 'bg-[var(--brand)]' },
  info: { pill: 'bg-[var(--brand-bg)] text-[var(--brand-text)] border-[var(--brand-border)]', dot: 'bg-[var(--brand)]' },
  neutral: { pill: 'bg-[var(--gray-bg)] text-[var(--gray-text)] border-[var(--gray-border)]', dot: 'bg-[var(--gray-dot)]' },
  success: { pill: 'bg-[var(--ok-bg)] text-[var(--ok-text)] border-[var(--ok-border)]', dot: 'bg-[var(--ok-dot)]' },
  warning: { pill: 'bg-[var(--warn-bg)] text-[var(--warn-text)] border-[var(--warn-border)]', dot: 'bg-[var(--warn-dot)]' },
  error: { pill: 'bg-[var(--err-bg)] text-[var(--err-text)] border-[var(--err-border)]', dot: 'bg-[var(--err-dot)]' },
};

export function Badge({ variant = 'default', children, className, noDot }: BadgeProps) {
  const v = variants[variant];
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 pl-[7px] pr-2 py-[2px] rounded-full border text-[12px] leading-[18px] font-medium whitespace-nowrap',
        v.pill,
        className,
      )}
    >
      {!noDot && <span className={cn('w-2 h-2 rounded-full flex-none', v.dot)} />}
      {children}
    </span>
  );
}
