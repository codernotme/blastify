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
import { sendMessages } from '@/app/api/api'

type FormData = {
  message: string
  deliveryMethod: 'whatsapp' | 'email'
}

const MainContent = () => {
  type Contact = {
    id: string
    name: string
    email: string
    phone: string
  }

  const [contacts, setContacts] = useState<Contact[]>([])
  const [selectedContacts, setSelectedContacts] = useState<string[]>([])
  const [statusMessage, setStatusMessage] = useState<string | null>(null)
  const { control, handleSubmit, reset } = useForm<FormData>()

  const handleFileUpload = (file: File) => {
    // Handle file upload logic here
    console.log(file)
  }

  const onSubmit = async (data: FormData) => {
    try {
      const payload = {
        contacts: selectedContacts
          .map(id => contacts.find(contact => contact.id === id))
          .filter((contact): contact is Contact => contact !== undefined)
          .map(contact => ({ value: contact.id })),
        message: data.message,
        method: data.deliveryMethod,
      }
      await sendMessages(payload)
      setStatusMessage("Messages sent successfully!")
    } catch {
      console.error("Failed to send messages. Please try again.")
      setStatusMessage("Failed to send messages. Please try again.")
    }
  }

  const handleClearAll = () => {
    setContacts([])
    setSelectedContacts([])
    reset()
    setStatusMessage(null)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {statusMessage && <div className="status-message">{statusMessage}</div>}
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