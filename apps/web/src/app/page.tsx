import Link from 'next/link';

export default function HomePage() {
  return (
    <main style={{ maxWidth: 880, margin: '4rem auto', padding: '0 1.5rem' }}>
      <h1>Adult Creator Tax &amp; Accounting Copilot</h1>
      <p>
        Aggregate fiat and crypto payouts across platforms, generate compliance
        evidence, and file 1099 / W-8BEN / VAT MOSS forms. Quantum-safe,
        OWASP-first, multi-cloud (Zeabur, Northflank, Scaleway, Exoscale).
      </p>
      <ul>
        <li>
          <Link href="/dashboard">Dashboard</Link>
        </li>
        <li>
          <Link href="/tax/1099">Generate a 1099</Link>
        </li>
        <li>
          <Link href="/tax/w8ben">Generate a W-8BEN</Link>
        </li>
        <li>
          <Link href="/tax/vat">EU VAT MOSS</Link>
        </li>
        <li>
          <Link href="/crypto/fifo">Crypto FIFO</Link>
        </li>
        <li>
          <Link href="/zk/age">ZK Age Proof</Link>
        </li>
      </ul>
    </main>
  );
}
