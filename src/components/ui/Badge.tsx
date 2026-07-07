import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'neutral';
  children: ReactNode;
  className?: string;
}

const variants = {
  default: 'bg-gray-100 text-gray-600',
  neutral: 'bg-gray-100 text-gray-500',
  success: 'bg-emerald-50 text-emerald-700 border border-emerald-100',
  warning: 'bg-amber-50 text-amber-700 border border-amber-100',
  error: 'bg-red-50 text-red-700 border border-red-100',
  info: 'bg-blue-50 text-blue-700 border border-blue-100',
};

export function Badge({ variant = 'default', children, className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium',
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
