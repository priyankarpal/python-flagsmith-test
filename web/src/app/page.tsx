'use client';

import { useEffect, useState } from 'react';
import { flagsmith } from '@/lib/flagsmith';

export default function Home() {
  const [enabled, setEnabled] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const init = async () => {
      await flagsmith.identify('demo-user', { plan: 'premium' });
      
      if (!mounted) return;
      
      const result = flagsmith.hasFeature('new_checkout_flow');
      setEnabled(result);
      setLoading(false);

      // Start realtime polling for updates
      flagsmith.startListening(5000);

      // Check for changes periodically as fallback
      const interval = setInterval(() => {
        if (!mounted) return;
        const current = flagsmith.hasFeature('new_checkout_flow');
        if (current !== enabled) setEnabled(current);
      }, 5000);

      return () => {
        clearInterval(interval);
        flagsmith.stopListening();
      };
    };

    init().catch(() => {
      if (mounted) setLoading(false);
    });

    return () => { mounted = false; };
  }, [enabled]);

  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center">
          Flagsmith Demo: Two Versions
        </h1>

        {enabled ? (
          <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg border border-green-200 dark:border-green-800">
            <h2 className="text-2xl font-semibold text-green-800 dark:text-green-200 mb-4">
              🎉 Version B (New Checkout Flow)
            </h2>
            <p className="text-green-700 dark:text-green-300">
              This user sees the <strong>new checkout flow</strong> because the feature flag
              <code className="bg-green-100 dark:bg-green-900 px-1 rounded">
                new_checkout_flow
              </code>
              is <strong>enabled</strong> for them.
            </p>
            <div className="mt-4 p-4 bg-white dark:bg-gray-800 rounded border">
              <p className="font-mono text-sm">
                New single-page checkout with saved payment methods
              </p>
            </div>
          </div>
        ) : (
          <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
            <h2 className="text-2xl font-semibold text-blue-800 dark:text-blue-200 mb-4">
              📦 Version A (Legacy Checkout)
            </h2>
            <p className="text-blue-700 dark:text-blue-300">
              This user sees the <strong>legacy checkout</strong> because the feature flag
              <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">
                new_checkout_flow
              </code>
              is <strong>disabled</strong> for them.
            </p>
            <div className="mt-4 p-4 bg-white dark:bg-gray-800 rounded border">
              <p className="font-mono text-sm">
                Multi-step checkout: Cart → Shipping → Payment → Review
              </p>
            </div>
          </div>
        )}

        <div className="mt-8 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <h3 className="font-semibold mb-2">How it works</h3>
          <ul className="text-sm space-y-1 text-gray-700 dark:text-gray-300">
            <li>Flag <code className="bg-gray-200 dark:bg-gray-700 px-1 rounded">new_checkout_flow</code> controlled in Flagsmith dashboard</li>
            <li>Segment override: enabled for <code className="bg-gray-200 dark:bg-gray-700 px-1 rounded">plan=premium</code></li>
            <li>User identified with traits → realtime updates via polling</li>
          </ul>
        </div>
      </div>
    </div>
  );
}