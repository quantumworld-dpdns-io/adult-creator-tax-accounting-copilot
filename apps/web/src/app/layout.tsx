import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Adult Creator Tax & Accounting Copilot',
  description:
    'Aggregate fiat/crypto payouts, generate compliance evidence, and file tax forms. Quantum-safe, OWASP-first, multi-cloud.',
  applicationName: 'Copilot',
  authors: [{ name: 'quantumworld-dpdns-io' }],
  keywords: ['tax', 'creator', 'compliance', 'quantum', 'zk', 'multi-cloud'],
  formatDetection: { email: false, address: false, telephone: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
