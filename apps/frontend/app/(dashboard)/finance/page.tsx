'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function FinancePage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to wallets page as default
    router.replace('/finance/wallets');
  }, [router]);

  return null;
}