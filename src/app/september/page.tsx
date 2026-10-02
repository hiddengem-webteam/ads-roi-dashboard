import { Inter } from 'next/font/google';
import SeptemberDashboard from '@/components/SeptemberDashboard';
import '@/components/july/theme.css';

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] });

export default function SeptemberPage() {
  return (
    <div className={`july-theme h-screen ${inter.variable}`}>
      <SeptemberDashboard />
    </div>
  );
}
