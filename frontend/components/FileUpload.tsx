import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File } from 'lucide-react'
import { uploadFile } from '@/app/api/api'

interface FileUploadProps {
  onFileUpload: (contacts: { value: string }[]) => void
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const [isUploading, setIsUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setIsUploading(true)
      try {
        const formData = new FormData()
        formData.append('file', acceptedFiles[0])
        const response = await uploadFile(formData, acceptedFiles[0])
        onFileUpload(response.contacts)
      } catch (error) {
        console.error('File upload failed:', error)
      } finally {
        setIsUploading(false)
      }
    }
  }, [onFileUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  })

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-6 sm:p-8 text-center cursor-pointer transition-colors ${
        isDragActive ? 'border-primary bg-primary/5' : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <input {...getInputProps()} />
      {isUploading ? (
        <div className="text-primary">
          <File className="mx-auto h-10 w-10 sm:h-12 sm:w-12 animate-pulse" />
          <p className="mt-2 text-sm sm:text-base">Uploading...</p>
        </div>
      ) : isDragActive ? (
        <div className="text-primary">
          <Upload className="mx-auto h-10 w-10 sm:h-12 sm:w-12" />
          <p className="mt-2 text-sm sm:text-base">Drop the file here</p>
        </div>
      ) : (
        <div>
          <Upload className="mx-auto h-10 w-10 sm:h-12 sm:w-12 text-gray-400" />
          <p className="mt-2 text-sm sm:text-base">Drag & drop a file here, or click to select a file</p>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">Supported formats: .xlsx, .csv, .pdf</p>
        </div>
      )}
    </div>
  )
}

export default FileUpload

