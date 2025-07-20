import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Shield, BookOpen, Phone, Calendar } from 'lucide-react';

const AboutPage = () => {
    const features = [
        {
            icon: Bot,
            title: 'AI-Powered Support',
            description: 'Advanced AI trained on Apple\'s official support documentation to provide accurate, helpful responses.'
        },
        {
            icon: Shield,
            title: 'Safety & Privacy',
            description: 'Built-in guardrails to protect your privacy and ensure safe, appropriate responses.'
        },
        {
            icon: BookOpen,
            title: 'Knowledge Base',
            description: 'Access to comprehensive Apple support information, FAQs, and troubleshooting guides.'
        },
        {
            icon: Phone,
            title: 'Voice Support',
            description: 'Get help through natural voice conversations using advanced speech recognition.'
        },
        {
            icon: Calendar,
            title: 'Meeting Scheduling',
            description: 'Schedule appointments with Apple Support when you need human assistance.'
        }
    ];

    return (
        <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="text-center mb-12">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold text-gray-900 mb-4"
                >
                    About Apple Support AI Agent
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-lg text-gray-600 max-w-2xl mx-auto"
                >
                    Your intelligent assistant for all things Apple. Get instant help with your Apple products and services through chat, voice, or schedule a meeting with support.
                </motion.p>
            </div>

            {/* Features */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                {features.map((feature, index) => {
                    const Icon = feature.icon;
                    return (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="card text-center"
                        >
                            <div className="w-12 h-12 bg-apple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                                <Icon size={24} className="text-apple-600" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                {feature.title}
                            </h3>
                            <p className="text-gray-600">
                                {feature.description}
                            </p>
                        </motion.div>
                    );
                })}
            </div>

            {/* How it works */}
            <div className="card mb-12">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                        <div className="w-16 h-16 bg-apple-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                            1
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Ask Your Question</h3>
                        <p className="text-gray-600">
                            Type your question or use voice to describe your Apple-related issue.
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="w-16 h-16 bg-apple-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                            2
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
                        <p className="text-gray-600">
                            Our AI searches through Apple's support documentation to find the best answer.
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="w-16 h-16 bg-apple-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                            3
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Get Help</h3>
                        <p className="text-gray-600">
                            Receive accurate, helpful responses with sources and confidence scores.
                        </p>
                    </div>
                </div>
            </div>

            {/* Safety & Privacy */}
            <div className="card mb-12">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Safety & Privacy</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <h3 className="font-semibold text-gray-900 mb-3">Privacy Protection</h3>
                        <ul className="space-y-2 text-gray-600">
                            <li>• No personal data is stored or shared</li>
                            <li>• Automatic detection and redaction of sensitive information</li>
                            <li>• Secure, encrypted communications</li>
                            <li>• Compliance with privacy regulations</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="font-semibold text-gray-900 mb-3">Safety Features</h3>
                        <ul className="space-y-2 text-gray-600">
                            <li>• Content filtering and moderation</li>
                            <li>• Detection of inappropriate requests</li>
                            <li>• Rate limiting to prevent abuse</li>
                            <li>• Automatic escalation for complex issues</li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Limitations */}
            <div className="card">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Important Limitations</h2>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                    <p className="text-yellow-800">
                        <strong>Note:</strong> This AI agent is designed to provide general information and guidance about Apple products and services. It cannot:
                    </p>
                </div>
                <ul className="space-y-3 text-gray-600">
                    <li>• Provide legal or financial advice</li>
                    <li>• Access your personal Apple account information</li>
                    <li>• Process warranty claims or repairs</li>
                    <li>• Handle billing or payment issues</li>
                    <li>• Replace official Apple Support for critical issues</li>
                </ul>
                <p className="mt-4 text-sm text-gray-500">
                    For account-specific issues, billing problems, or complex technical support, please contact Apple Support directly.
                </p>
            </div>
        </div>
    );
};

export default AboutPage; 