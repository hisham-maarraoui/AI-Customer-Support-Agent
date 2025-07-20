import React from 'react';
import { ExternalLink, FileText, Globe } from 'lucide-react';

const SourcesList = ({ sources, confidence }) => {
    if (!sources || sources.length === 0) {
        return (
            <div className="text-center text-gray-500 py-8">
                <FileText size={48} className="mx-auto mb-4 text-gray-300" />
                <p>No sources available</p>
            </div>
        );
    }

    const getConfidenceColor = (conf) => {
        if (conf >= 0.7) return 'text-green-600';
        if (conf >= 0.4) return 'text-yellow-600';
        return 'text-red-600';
    };

    const getConfidenceText = (conf) => {
        if (conf >= 0.7) return 'High';
        if (conf >= 0.4) return 'Medium';
        return 'Low';
    };

    return (
        <div className="space-y-4">
            {/* Confidence Score */}
            {confidence !== undefined && (
                <div className="bg-gray-50 rounded-lg p-3">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">Confidence</span>
                        <span className={`text-sm font-semibold ${getConfidenceColor(confidence)}`}>
                            {getConfidenceText(confidence)} ({Math.round(confidence * 100)}%)
                        </span>
                    </div>
                    <div className="mt-2 bg-gray-200 rounded-full h-2">
                        <div
                            className={`h-2 rounded-full transition-all duration-300 ${confidence >= 0.7
                                    ? 'bg-green-500'
                                    : confidence >= 0.4
                                        ? 'bg-yellow-500'
                                        : 'bg-red-500'
                                }`}
                            style={{ width: `${confidence * 100}%` }}
                        />
                    </div>
                </div>
            )}

            {/* Sources */}
            <div>
                <h4 className="text-sm font-medium text-gray-700 mb-3">
                    Sources ({sources.length})
                </h4>
                <div className="space-y-3">
                    {sources.map((source, index) => (
                        <div
                            key={index}
                            className="bg-gray-50 rounded-lg p-3 border border-gray-200"
                        >
                            {/* Source Title */}
                            <div className="flex items-start justify-between mb-2">
                                <h5 className="text-sm font-medium text-gray-900 line-clamp-2">
                                    {source.title || 'Apple Support Documentation'}
                                </h5>
                                {source.url && (
                                    <a
                                        href={source.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex-shrink-0 ml-2 text-apple-600 hover:text-apple-700"
                                    >
                                        <ExternalLink size={14} />
                                    </a>
                                )}
                            </div>

                            {/* Source URL */}
                            {source.url && (
                                <div className="flex items-center text-xs text-gray-500 mb-2">
                                    <Globe size={12} className="mr-1" />
                                    <span className="truncate">{source.url}</span>
                                </div>
                            )}

                            {/* Source Metadata */}
                            <div className="flex items-center justify-between text-xs text-gray-500">
                                <div className="flex items-center space-x-3">
                                    {source.product && (
                                        <span className="bg-apple-100 text-apple-800 px-2 py-1 rounded">
                                            {source.product}
                                        </span>
                                    )}
                                    {source.content_type && (
                                        <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded">
                                            {source.content_type}
                                        </span>
                                    )}
                                </div>
                                {source.relevance_score !== undefined && (
                                    <span className="text-gray-400">
                                        {Math.round(source.relevance_score * 100)}% relevant
                                    </span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Disclaimer */}
            <div className="text-xs text-gray-500 bg-blue-50 p-3 rounded-lg">
                <p>
                    Sources are from Apple's official support documentation.
                    Always verify information with official Apple channels for critical issues.
                </p>
            </div>
        </div>
    );
};

export default SourcesList; 