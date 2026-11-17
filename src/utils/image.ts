/**
 * Converte e redimensiona imagens (incluindo fotos pesadas ou HEIC de celular)
 * para um JPEG leve (máx. 1024px) antes do envio ao servidor/IA.
 */
export async function normalizeImageFile(file: File): Promise<File> {
  if (!file) return file;
  // Se já for JPEG/PNG/WEBP leve (< 400 KB), evita recompressão desnecessária
  const webSafe = ["image/jpeg", "image/png", "image/webp"];
  if (webSafe.includes(file.type) && file.size <= 400 * 1024) {
    return file;
  }

  return new Promise((resolve) => {
    const objectUrl = URL.createObjectURL(file);
    const img = new Image();

    img.onload = () => {
      try {
        const maxDim = 1024;
        let width = img.naturalWidth || img.width;
        let height = img.naturalHeight || img.height;

        if (!width || !height) {
          URL.revokeObjectURL(objectUrl);
          resolve(file);
          return;
        }

        if (width > maxDim || height > maxDim) {
          if (width >= height) {
            height = Math.round((height * maxDim) / width);
            width = maxDim;
          } else {
            width = Math.round((width * maxDim) / height);
            height = maxDim;
          }
        }

        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        if (!ctx) {
          URL.revokeObjectURL(objectUrl);
          resolve(file);
          return;
        }

        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob(
          (blob) => {
            URL.revokeObjectURL(objectUrl);
            if (!blob) {
              resolve(file);
              return;
            }
            const baseName = file.name.replace(/\.[^.]+$/, "") || "produto";
            const converted = new File([blob], `${baseName}.jpg`, {
              type: "image/jpeg",
              lastModified: Date.now(),
            });
            resolve(converted);
          },
          "image/jpeg",
          0.85,
        );
      } catch {
        URL.revokeObjectURL(objectUrl);
        resolve(file);
      }
    };

    img.onerror = () => {
      URL.revokeObjectURL(objectUrl);
      resolve(file);
    };

    img.src = objectUrl;
  });
}
