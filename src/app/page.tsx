import { Inter } from 'next/font/google';
import Dashboard from '@/components/Dashboard';
import '@/components/july/theme.css';

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] });

export default function Home() {
  return (
    <div className={`july-theme h-screen ${inter.variable}`}>
      <Dashboard />
    </div>
  );
}
