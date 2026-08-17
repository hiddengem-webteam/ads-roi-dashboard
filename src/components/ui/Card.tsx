'use client';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface CardProps {
  className?: string;
  children: ReactNode;
}

export function Card({ className, children }: CardProps) {
  return (
    <div
      className={cn(
        'bg-[var(--surface)] rounded-[16px] border border-[var(--border)] shadow-[0_8px_22px_rgba(15,23,42,.04)]',
        className,
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children }: CardProps) {
  return <div className={cn('px-6 py-5 border-b border-[var(--border)]', className)}>{children}</div>;
}

export function CardTitle({ className, children }: CardProps) {
  return (
    <h3 className={cn('text-[12px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]', className)}>
      {children}
    </h3>
  );
}

export function CardContent({ className, children }: CardProps) {
  return <div className={cn('px-6 py-5', className)}>{children}</div>;
}

export function StatCard({
  label,
  value,
  sub,
  accent,
  className,
}: {
  label: string;
  value: string | number;
  sub?: string;
  accent?: boolean;
  className?: string;
}) {
  return (
    <div
      className={cn(
        'rounded-[12px] px-5 py-4',
        accent ? 'bg-[var(--brand)] text-white' : 'bg-[var(--fill-gray)] border border-[var(--border)]',
        className,
      )}
    >
      <p className={cn('text-[12px] font-medium mb-2', accent ? 'text-white/70' : 'text-[var(--muted)]')}>{label}</p>
      <p className={cn('text-[20px] font-bold tracking-[-0.01em] july-tabular', accent ? 'text-white' : 'text-[var(--foreground)]')}>
        {value}
      </p>
      {sub && <p className={cn('text-[12px] mt-1', accent ? 'text-white/60' : 'text-[var(--muted-soft)]')}>{sub}</p>}
    </div>
  );
}
