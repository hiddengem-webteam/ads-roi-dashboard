import { Inter } from 'next/font/google';
import JulyDashboard from '@/components/JulyDashboard';
import '@/components/july/theme.css';

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] });

export default function JulyPage() {
  return (
    <div className={`july-theme h-screen ${inter.variable}`}>
      <JulyDashboard />
    </div>
  );
}
