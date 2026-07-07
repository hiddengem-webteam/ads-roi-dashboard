'use client';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface CardProps {
  className?: string;
  children: ReactNode;
}

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn('bg-white rounded-2xl border border-gray-100 shadow-[0_1px_4px_rgba(0,0,0,0.06)]', className)}>
      {children}
    </div>
  );
}

export function CardHeader({ className, children }: CardProps) {
  return <div className={cn('px-6 py-5 border-b border-gray-100', className)}>{children}</div>;
}

export function CardTitle({ className, children }: CardProps) {
  return (
    <h3 className={cn('text-xs font-semibold text-gray-400 uppercase tracking-widest', className)}>
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
        'rounded-xl px-5 py-4',
        accent ? 'bg-gray-900 text-white' : 'bg-gray-50 border border-gray-100',
        className,
      )}
    >
      <p className={cn('text-xs font-medium mb-2', accent ? 'text-gray-400' : 'text-gray-500')}>{label}</p>
      <p className={cn('text-2xl font-bold tracking-tight', accent ? 'text-white' : 'text-gray-900')}>{value}</p>
      {sub && <p className={cn('text-xs mt-1', accent ? 'text-gray-500' : 'text-gray-400')}>{sub}</p>}
    </div>
  );
}
