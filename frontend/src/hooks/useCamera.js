import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Single-shot camera capture. Does NOT stream frames to the backend.
 */
export function useCamera() {
  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const [isOpen, setIsOpen] = useState(false)
  const [error, setError] = useState(null)
  const [capturedUrl, setCapturedUrl] = useState(null)
  const [capturedBlob, setCapturedBlob] = useState(null)

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop())
      streamRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
    setIsOpen(false)
  }, [])

  const openCamera = useCallback(async () => {
    setError(null)
    setCapturedUrl(null)
    setCapturedBlob(null)
    stopCamera()

    if (!navigator.mediaDevices?.getUserMedia) {
      setError(
        'Camera is not supported in this browser. Use Upload Image instead.',
      )
      return
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
          facingMode: { ideal: 'environment' },
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
      })
      streamRef.current = stream
      setIsOpen(true)
      // Attach after state update / next paint
      requestAnimationFrame(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.play().catch(() => {})
        }
      })
    } catch (err) {
      const name = err?.name || ''
      if (name === 'NotAllowedError' || name === 'PermissionDeniedError') {
        setError(
          'Camera permission is required to scan an image. If your camera is unavailable, use Upload Image instead.',
        )
      } else if (name === 'NotFoundError' || name === 'DevicesNotFoundError') {
        setError(
          'No camera was found on this device. Use Upload Image instead.',
        )
      } else {
        setError(
          'Camera could not be opened. If your camera is unavailable, use Upload Image instead.',
        )
      }
      setIsOpen(false)
    }
  }, [stopCamera])

  const captureImage = useCallback(async () => {
    const video = videoRef.current
    if (!video || !video.videoWidth) {
      setError('Camera preview is not ready yet. Please wait a moment.')
      return null
    }
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0)
    const blob = await new Promise((resolve) =>
      canvas.toBlob(resolve, 'image/jpeg', 0.92),
    )
    if (!blob) {
      setError('Could not capture image. Please try again.')
      return null
    }
    const url = URL.createObjectURL(blob)
    setCapturedBlob(blob)
    setCapturedUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return url
    })
    stopCamera()
    return blob
  }, [stopCamera])

  const retake = useCallback(() => {
    setCapturedBlob(null)
    setCapturedUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return null
    })
    openCamera()
  }, [openCamera])

  const clearCapture = useCallback(() => {
    setCapturedBlob(null)
    setCapturedUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return null
    })
  }, [])

  useEffect(() => {
    return () => {
      stopCamera()
      if (capturedUrl) URL.revokeObjectURL(capturedUrl)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return {
    videoRef,
    isOpen,
    error,
    setError,
    capturedUrl,
    capturedBlob,
    openCamera,
    stopCamera,
    captureImage,
    retake,
    clearCapture,
  }
}
