'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ThemeToggle } from '@/components/theme-toggle'
import MainContent from '@/components/MainContent'

export default function Dashboard() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <header className="mb-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Blastify</h1>
          <ThemeToggle />
        </header>
        <MainContent />
      </motion.div>
    </div>
  )
}

