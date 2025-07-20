import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock, Phone, Video, MapPin } from 'lucide-react';

const SchedulePage = () => {
    return (
        <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold text-gray-900 mb-2"
                >
                    Schedule Support Meeting
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-gray-600"
                >
                    Book a meeting with Apple Support when you need human assistance
                </motion.p>
            </div>

            <div className="card">
                <div className="text-center py-12">
                    <Calendar size={64} className="mx-auto mb-4 text-gray-400" />
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                        Meeting Scheduling Coming Soon
                    </h2>
                    <p className="text-gray-600 mb-6">
                        This feature will allow you to schedule phone calls, video meetings, or in-person appointments with Apple Support representatives.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Phone size={16} />
                            <span>Phone Support</span>
                        </div>
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Video size={16} />
                            <span>Video Calls</span>
                        </div>
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <MapPin size={16} />
                            <span>In-Person</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SchedulePage; 