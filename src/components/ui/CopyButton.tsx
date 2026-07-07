'use client';
import { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { Button } from './Button';
import { copyToClipboard } from '@/lib/utils';

interface CopyButtonProps {
  getText: () => string;
  label?: string;
}

export function CopyButton({ getText, label = 'Copy list' }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await copyToClipboard(getText());
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // ignore
    }
  };

  return (
    <Button variant="outline" size="sm" onClick={handleCopy}>
      {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5" />}
      {copied ? 'Copied!' : label}
    </Button>
  );
}
