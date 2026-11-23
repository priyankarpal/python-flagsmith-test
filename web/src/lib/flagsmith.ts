'use client';

import { createFlagsmithInstance } from 'flagsmith';

export const flagsmith = createFlagsmithInstance();

if (typeof window !== 'undefined') {
  flagsmith.init({
    environmentID: process.env.NEXT_PUBLIC_FLAGSMITH_ENV_ID!,
    api: process.env.NEXT_PUBLIC_FLAGSMITH_API_URL,
    realtime: true,
  });
}