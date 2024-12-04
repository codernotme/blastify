import { NextResponse } from 'next/server'
import * as XLSX from 'xlsx'

export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 })
    }

    const buffer = await file.arrayBuffer()
    const workbook = XLSX.read(buffer, { type: 'array' })
    const sheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[sheetName]
    const data = XLSX.utils.sheet_to_json(worksheet)

    const contacts = data.map((row: any, index) => ({
      id: `${index + 1}`,
      name: row.name || 'Unknown',
      email: row.email || '',
      phone: row.phone || '',
    }))

    return NextResponse.json({ contacts })
  } catch (error) {
    console.error('Error processing file:', error)
    return NextResponse.json({ error: 'Error processing file' }, { status: 500 })
  }
}

