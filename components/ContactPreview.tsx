import { useState } from 'react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Checkbox } from '@/components/ui/checkbox'

interface Contact {
  id: string
  name: string
  email: string
  phone: string
}

interface ContactPreviewProps {
  contacts: Contact[]
  selectedContacts: string[]
  setSelectedContacts: (contacts: string[]) => void
}

const ContactPreview: React.FC<ContactPreviewProps> = ({
  contacts,
  selectedContacts,
  setSelectedContacts,
}) => {
  const [selectAll, setSelectAll] = useState(false)

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedContacts([])
    } else {
      setSelectedContacts(contacts.map(contact => contact.id))
    }
    setSelectAll(!selectAll)
  }

  const handleSelectContact = (contactId: string) => {
    if (selectedContacts.includes(contactId)) {
      setSelectedContacts(selectedContacts.filter(id => id !== contactId))
    } else {
      setSelectedContacts([...selectedContacts, contactId])
    }
  }

  return (
    <div className="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[50px]">
              <Checkbox
                checked={selectAll}
                onCheckedChange={handleSelectAll}
              />
            </TableHead>
            <TableHead>Name</TableHead>
            <TableHead className="hidden sm:table-cell">Email</TableHead>
            <TableHead className="hidden md:table-cell">Phone</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {contacts.map((contact) => (
            <TableRow key={contact.id}>
              <TableCell>
                <Checkbox
                  checked={selectedContacts.includes(contact.id)}
                  onCheckedChange={() => handleSelectContact(contact.id)}
                />
              </TableCell>
              <TableCell>{contact.name}</TableCell>
              <TableCell className="hidden sm:table-cell">{contact.email}</TableCell>
              <TableCell className="hidden md:table-cell">{contact.phone}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

export default ContactPreview

