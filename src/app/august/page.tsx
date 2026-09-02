import { Inter } from 'next/font/google';
import AugustDashboard from '@/components/AugustDashboard';
import '@/components/july/theme.css';

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] });

export default function AugustPage() {
  return (
    <div className={`july-theme h-screen ${inter.variable}`}>
      <AugustDashboard />
    </div>
  );
}
