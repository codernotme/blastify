'use client'

import { useState } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { motion } from 'framer-motion'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import FileUploadCard from './FileUploadCard'
import ContactsCard from './ContactsCard'
import MessageCard from './MessageCard'
import DeliveryMethodCard from './DeliveryMethodCard'
import ActionButtons from './ActionButtons'

type FormData = {
  message: string
  deliveryMethod: 'whatsapp' | 'email'
}

const MainContent = () => {
  const [file, setFile] = useState<File | null>(null)
  const [contacts, setContacts] = useState<any[]>([])
  const [selectedContacts, setSelectedContacts] = useState<string[]>([])
  const { control, handleSubmit, reset } = useForm<FormData>()

  const onSubmit = async (data: FormData) => {
    try {
      // Simulating API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      console.log("Messages sent successfully!")
      // Here you would typically show a success message to the user
    } catch (error) {
      console.error("Failed to send messages. Please try again.")
      // Here you would typically show an error message to the user
    }
  }

  const handleFileUpload = async (file: File) => {
    setFile(file)
    // Simulating file processing
    await new Promise(resolve => setTimeout(resolve, 2000))
    setContacts([
      { id: '1', name: 'John Doe', email: 'john@example.com', phone: '+1234567890' },
      { id: '2', name: 'Jane Smith', email: 'jane@example.com', phone: '+0987654321' },
    ])
  }

  const handleClearAll = () => {
    setFile(null)
    setContacts([])
    setSelectedContacts([])
    reset()
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <Tabs defaultValue="upload" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="upload">Upload</TabsTrigger>
          <TabsTrigger value="contacts">Contacts</TabsTrigger>
          <TabsTrigger value="message">Message</TabsTrigger>
        </TabsList>
        <TabsContent value="upload">
          <FileUploadCard onFileUpload={handleFileUpload} />
        </TabsContent>
        <TabsContent value="contacts">
          <ContactsCard
            contacts={contacts}
            selectedContacts={selectedContacts}
            setSelectedContacts={setSelectedContacts}
          />
        </TabsContent>
        <TabsContent value="message">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <Controller
              name="message"
              control={control}
              rules={{ required: 'Message is required' }}
              render={({ field, fieldState: { error } }) => (
                <MessageCard {...field} error={error} />
              )}
            />
            <Controller
              name="deliveryMethod"
              control={control}
              rules={{ required: 'Delivery method is required' }}
              render={({ field }) => (
                <DeliveryMethodCard {...field} />
              )}
            />
            <ActionButtons onClearAll={handleClearAll} />
          </form>
        </TabsContent>
      </Tabs>
    </motion.div>
  )
}

export default MainContent

