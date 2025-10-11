'use client';
import { Navbar } from '@/components/navbar';
import { Debug } from '@/components/debug';
import { Pannel } from '@/components/pannel';

export default function Home() {
  return (
    <div
      className="h-screen bg-gradient-to-br from-orange-100 via-yellow-50 to-white relative overflow-hidden"
      style={{
        backgroundImage: `
          repeating-linear-gradient(120deg, rgba(247, 207, 118, 0.07) 0 10px, transparent 10px 20px),
          url('https://www.transparenttextures.com/patterns/hexellence.png')
        `,
        backgroundBlendMode: 'lighten',
      }}
    >
      <span
        style={{
          position: 'absolute',
          left: '4%',
          top: '8%',
          fontSize: '2.6rem',
          opacity: '0.14',
          pointerEvents: 'none',
        }}
        aria-hidden="true"
      >
        🎃
      </span>
      <span
        style={{
          position: 'absolute',
          left: '89%',
          top: '17%',
          fontSize: '2.2rem',
          opacity: '0.12',
          pointerEvents: 'none',
        }}
        aria-hidden="true"
      >
        🎃
      </span>
      <span
        style={{
          position: 'absolute',
          left: '14%',
          top: '80%',
          fontSize: '2.8rem',
          opacity: '0.09',
          pointerEvents: 'none',
        }}
        aria-hidden="true"
      >
        👻
      </span>
      <span
        style={{
          position: 'absolute',
          left: '70%',
          top: '89%',
          fontSize: '2.5rem',
          opacity: '0.10',
          pointerEvents: 'none',
        }}
        aria-hidden="true"
      >
        🦇
      </span>
      <Debug />
      <Navbar />
      <div className="font-sans flex flex-col">
        <Pannel />
      </div>
    </div>
  );
}
