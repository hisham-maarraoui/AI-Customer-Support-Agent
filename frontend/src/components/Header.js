import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    MessageCircle,
    Phone,
    Calendar,
    BookOpen,
    Info,
    Menu,
    X
} from 'lucide-react';
import DarkModeToggle from './DarkModeToggle';

const Header = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const location = useLocation();

    const navigation = [
        { name: 'Chat', href: '/', icon: MessageCircle },
        { name: 'Voice', href: '/voice', icon: Phone },
        { name: 'Schedule', href: '/schedule', icon: Calendar },
        { name: 'Knowledge', href: '/knowledge', icon: BookOpen },
        { name: 'About', href: '/about', icon: Info },
    ];

    const isActive = (path) => location.pathname === path;

    return (
        <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
            <div className="container mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2">
                        <span className="text-xl font-semibold text-gray-900 dark:text-white">
                            Apple Support AI
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex space-x-8">
                        {navigation.map((item) => {
                            const Icon = item.icon;
                            return (
                                <Link
                                    key={item.name}
                                    to={item.href}
                                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${isActive(item.href)
                                        ? 'text-apple-600 bg-apple-50 dark:bg-apple-900/20'
                                        : 'text-gray-600 dark:text-gray-300 hover:text-apple-600 dark:hover:text-apple-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                                        }`}
                                >
                                    <Icon size={18} />
                                    <span>{item.name}</span>
                                </Link>
                            );
                        })}
                    </nav>

                    {/* Dark Mode Toggle */}
                    <div className="hidden md:flex items-center space-x-4">
                        <DarkModeToggle />
                    </div>

                    {/* Mobile menu button and dark mode toggle */}
                    <div className="md:hidden flex items-center space-x-2">
                        <DarkModeToggle />
                        <button
                            className="p-2 rounded-md text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800"
                            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        >
                            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>
                </div>

                {/* Mobile Navigation */}
                {isMobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden border-t border-gray-200 dark:border-gray-700"
                    >
                        <div className="px-2 pt-2 pb-3 space-y-1">
                            {navigation.map((item) => {
                                const Icon = item.icon;
                                return (
                                    <Link
                                        key={item.name}
                                        to={item.href}
                                        className={`flex items-center space-x-3 px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${isActive(item.href)
                                            ? 'text-apple-600 bg-apple-50 dark:bg-apple-900/20'
                                            : 'text-gray-600 dark:text-gray-300 hover:text-apple-600 dark:hover:text-apple-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                                            }`}
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        <Icon size={20} />
                                        <span>{item.name}</span>
                                    </Link>
                                );
                            })}
                        </div>
                    </motion.div>
                )}
            </div>
        </header>
    );
};

export default Header; 