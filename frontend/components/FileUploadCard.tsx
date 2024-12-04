import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import FileUpload from './FileUpload'

interface FileUploadCardProps {
  onFileUpload: (file: File) => void
}

const FileUploadCard: React.FC<FileUploadCardProps> = ({ onFileUpload }) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Upload Contacts</CardTitle>
      </CardHeader>
      <CardContent>
        <FileUpload onFileUpload={onFileUpload} />
      </CardContent>
    </Card>
  )
}

export default FileUploadCard

