import React from 'react';
import Link from 'next/link';
import { useDebugStore } from '@/libs/zustand/debug';
import { Button } from './ui/button';
import { APP_NAME } from '@/constants';

const pumpkinEmoji = (
  <span role="img" aria-label="pumpkin" className="mr-2">
    🎃
  </span>
);

const bat = (
  <span role="img" aria-label="bat" className="ml-2">
    🦇
  </span>
);

export const Navbar = () => {
  const { triggerDebugOpen } = useDebugStore();

  return (
    <nav className="w-full bg-gradient-to-r from-orange-900 via-orange-700 to-black border-b border-orange-900 shadow-lg py-3 px-8 flex justify-between items-center relative">
      {/* Spider web effect with absolute element */}
      <div className="absolute inset-0 pointer-events-none">
        <svg
          width="100%"
          height="60"
          viewBox="0 0 500 60"
          className="w-full h-16 opacity-30"
        >
          <path
            d="M0,50 Q125,10 250,50 Q375,90 500,50"
            stroke="#fff8e1"
            strokeWidth="2"
            fill="transparent"
          />
          <path
            d="M0,58 Q125,49 250,58 Q375,67 500,58"
            stroke="#fff8e1"
            strokeWidth="1"
            fill="transparent"
          />
          <path d="M250,0 L250,58" stroke="#fff8e1" strokeWidth="1" />
          <path d="M125,10 L125,58" stroke="#fff8e1" strokeWidth="1" />
          <path d="M375,10 L375,58" stroke="#fff8e1" strokeWidth="1" />
        </svg>
      </div>
      <div className="relative z-10 flex items-center text-xl font-bold text-[#fff8e1] tracking-widest drop-shadow-md">
        {pumpkinEmoji}
        {APP_NAME}
        <span
          className="ml-2 text-orange-200 font-extrabold animate-pulse"
          style={{ textShadow: '0 0 8px #ff9700' }}
        >
          Halloween
        </span>
        {bat}
      </div>
      <ul className="relative z-10 flex gap-6 items-center">
        <li>
          <Link
            href="/"
            className="text-orange-100 hover:text-orange-300 font-medium transition-colors"
          >
            Home
          </Link>
        </li>
        <li>
          <Link
            href="https://github.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-orange-100 hover:text-orange-300 font-medium transition-colors"
          >
            GitHub
          </Link>
        </li>
        <li>
          <Button
            variant="outline"
            onClick={triggerDebugOpen}
            className="border-orange-400 hover:bg-orange-900 text-orange-200 hover:text-orange-100"
            style={{ boxShadow: '0 2px 8px #ff980080' }}
          >
            👻 Debug
          </Button>
        </li>
      </ul>
    </nav>
  );
};
