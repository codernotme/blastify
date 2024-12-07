import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import ContactPreview from './ContactPreview'

interface ContactsCardProps {
  contacts: { id: string; name: string; email: string; phone: string }[]
  selectedContacts: string[]
  setSelectedContacts: (contacts: string[]) => void
}

const ContactsCard: React.FC<ContactsCardProps> = ({
  contacts,
  selectedContacts,
  setSelectedContacts,
}) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Contacts</CardTitle>
      </CardHeader>
      <CardContent>
        <ContactPreview
          contacts={contacts}
          selectedContacts={selectedContacts}
          setSelectedContacts={setSelectedContacts}
        />
      </CardContent>
    </Card>
  )
}

export default ContactsCard

