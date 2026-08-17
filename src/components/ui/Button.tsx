'use client';
import { cn } from '@/lib/utils';
import { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  children: ReactNode;
}

const variants = {
  default: 'bg-[var(--brand)] text-white hover:bg-[var(--brand-deep)]',
  outline: 'bg-white border border-[var(--border-strong)] text-[var(--foreground)] hover:bg-[var(--fill-cool)]',
  ghost: 'text-[var(--brand)] hover:bg-[var(--fill-blue)]',
  destructive: 'bg-[var(--danger)] text-white hover:bg-[#b91c1c]',
};

const sizes = {
  sm: 'px-3 py-1.5 text-[12px]',
  md: 'px-4 py-2.5 text-[14px]',
  lg: 'px-5 py-3 text-[16px]',
};

export function Button({ variant = 'default', size = 'md', className, children, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center gap-1.5 rounded-[10px] font-semibold transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}
