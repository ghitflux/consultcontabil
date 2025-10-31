'use client';

import { useState } from 'react';
import { Button, Tooltip } from '@/heroui';
import { CheckIcon, CopyIcon } from '@/lib/icons';

interface SnippetCopyProps {
  text: string;
  label?: string;
}

export function SnippetCopy({ text, label }: SnippetCopyProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="inline-flex items-center gap-2">
      <span className="font-mono text-sm">{label || text}</span>
      <Tooltip content={copied ? 'Copiado!' : 'Copiar'}>
        <Button
          size="sm"
          variant="light"
          isIconOnly
          onPress={handleCopy}
          className="min-w-unit-6 h-6 w-6"
        >
          {copied ? (
            <CheckIcon className="h-4 w-4" />
          ) : (
            <CopyIcon className="h-4 w-4" />
          )}
        </Button>
      </Tooltip>
    </div>
  );
}
