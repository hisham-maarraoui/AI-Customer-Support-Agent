import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Phone, PhoneOff, Mic, MicOff, Volume2, Settings } from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const VoicePage = () => {
    const [isCallActive, setIsCallActive] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const [callDuration, setCallDuration] = useState(0);
    const [sessionId, setSessionId] = useState(null);
    const [phoneNumber, setPhoneNumber] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

    useEffect(() => {
        let interval;
        if (isCallActive) {
            interval = setInterval(() => {
                setCallDuration(prev => prev + 1);
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isCallActive]);

    const formatDuration = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    const startVoiceSession = async () => {
        if (!phoneNumber.trim()) {
            toast.error('Please enter a phone number');
            return;
        }

        setIsLoading(true);
        try {
            const response = await axios.post(`${API_BASE_URL}/api/voice/start`, {
                phone_number: phoneNumber,
                user_id: 'anonymous',
            });

            setSessionId(response.data.session_id);
            setIsCallActive(true);
            setCallDuration(0);
            toast.success('Voice session started!');
        } catch (error) {
            console.error('Error starting voice session:', error);
            toast.error('Failed to start voice session');
        } finally {
            setIsLoading(false);
        }
    };

    const endVoiceSession = async () => {
        if (!sessionId) return;

        setIsLoading(true);
        try {
            await axios.post(`${API_BASE_URL}/api/voice/end`, {
                session_id: sessionId,
                reason: 'user_ended',
            });

            setIsCallActive(false);
            setSessionId(null);
            toast.success('Voice session ended');
        } catch (error) {
            console.error('Error ending voice session:', error);
            toast.error('Failed to end voice session');
        } finally {
            setIsLoading(false);
        }
    };

    const toggleRecording = () => {
        setIsRecording(!isRecording);
        toast.success(isRecording ? 'Recording stopped' : 'Recording started');
    };

    return (
        <div className="max-w-2xl mx-auto">
            {/* Header */}
            <div className="text-center mb-8">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold text-gray-900 mb-2"
                >
                    Voice Support
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-gray-600"
                >
                    Get help through voice calls with our AI assistant
                </motion.p>
            </div>

            {/* Main Voice Interface */}
            <div className="card">
                {/* Call Status */}
                <div className="text-center mb-8">
                    <div className={`w-24 h-24 mx-auto rounded-full flex items-center justify-center mb-4 ${isCallActive ? 'bg-green-100' : 'bg-gray-100'
                        }`}>
                        {isCallActive ? (
                            <Phone className={`w-12 h-12 ${isCallActive ? 'text-green-600' : 'text-gray-400'}`} />
                        ) : (
                            <PhoneOff className="w-12 h-12 text-gray-400" />
                        )}
                    </div>

                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                        {isCallActive ? 'Call in Progress' : 'Ready to Call'}
                    </h2>

                    {isCallActive && (
                        <p className="text-2xl font-mono text-green-600">
                            {formatDuration(callDuration)}
                        </p>
                    )}
                </div>

                {/* Phone Number Input */}
                {!isCallActive && (
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Phone Number
                        </label>
                        <input
                            type="tel"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                            placeholder="+1 (555) 123-4567"
                            className="input-field"
                            disabled={isLoading}
                        />
                        <p className="text-xs text-gray-500 mt-1">
                            Enter your phone number to receive a call from our AI assistant
                        </p>
                    </div>
                )}

                {/* Call Controls */}
                <div className="flex justify-center space-x-4 mb-6">
                    {!isCallActive ? (
                        <button
                            onClick={startVoiceSession}
                            disabled={isLoading || !phoneNumber.trim()}
                            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isLoading ? (
                                <div className="flex items-center">
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                    Starting...
                                </div>
                            ) : (
                                <div className="flex items-center">
                                    <Phone size={18} className="mr-2" />
                                    Start Call
                                </div>
                            )}
                        </button>
                    ) : (
                        <button
                            onClick={endVoiceSession}
                            disabled={isLoading}
                            className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 disabled:opacity-50"
                        >
                            {isLoading ? (
                                <div className="flex items-center">
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                    Ending...
                                </div>
                            ) : (
                                <div className="flex items-center">
                                    <PhoneOff size={18} className="mr-2" />
                                    End Call
                                </div>
                            )}
                        </button>
                    )}
                </div>

                {/* Recording Controls */}
                {isCallActive && (
                    <div className="border-t border-gray-200 pt-6">
                        <div className="flex items-center justify-center space-x-4">
                            <button
                                onClick={toggleRecording}
                                className={`p-3 rounded-full transition-colors duration-200 ${isRecording
                                        ? 'bg-red-100 text-red-600'
                                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                    }`}
                            >
                                {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
                            </button>

                            <div className="flex items-center space-x-2">
                                <Volume2 size={16} className="text-gray-400" />
                                <span className="text-sm text-gray-600">Voice Level</span>
                            </div>
                        </div>

                        {isRecording && (
                            <div className="mt-4 text-center">
                                <div className="voice-recording w-4 h-4 bg-red-500 rounded-full mx-auto"></div>
                                <p className="text-sm text-red-600 mt-2">Recording...</p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Features */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-center"
                >
                    <div className="w-12 h-12 bg-apple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <Phone size={24} className="text-apple-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Voice Calls</h3>
                    <p className="text-sm text-gray-600">
                        Get help through natural voice conversations
                    </p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="text-center"
                >
                    <div className="w-12 h-12 bg-apple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <Settings size={24} className="text-apple-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Smart Routing</h3>
                    <p className="text-sm text-gray-600">
                        Intelligent call routing to the right support
                    </p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="text-center"
                >
                    <div className="w-12 h-12 bg-apple-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <Mic size={24} className="text-apple-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Voice Recognition</h3>
                    <p className="text-sm text-gray-600">
                        Advanced speech recognition for accurate help
                    </p>
                </motion.div>
            </div>

            {/* Instructions */}
            <div className="mt-8 card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    How Voice Support Works
                </h3>
                <div className="space-y-3 text-sm text-gray-600">
                    <div className="flex items-start space-x-3">
                        <div className="w-6 h-6 bg-apple-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                            1
                        </div>
                        <p>Enter your phone number and click "Start Call"</p>
                    </div>
                    <div className="flex items-start space-x-3">
                        <div className="w-6 h-6 bg-apple-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                            2
                        </div>
                        <p>Our AI assistant will call you and greet you</p>
                    </div>
                    <div className="flex items-start space-x-3">
                        <div className="w-6 h-6 bg-apple-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                            3
                        </div>
                        <p>Ask your question naturally and get help</p>
                    </div>
                    <div className="flex items-start space-x-3">
                        <div className="w-6 h-6 bg-apple-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                            4
                        </div>
                        <p>Click "End Call" when you're finished</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VoicePage; 