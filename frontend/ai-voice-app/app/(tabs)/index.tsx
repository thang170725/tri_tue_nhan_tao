import React, { useState } from "react";
import { View, Button, Text, StyleSheet } from "react-native";
import { Audio } from "expo-av";

export default function App() {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [uri, setUri] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  // Bắt đầu ghi âm
  const startRecording = async () => {
    try {
      console.log("Yêu cầu quyền micro...");
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });

      console.log("Bắt đầu ghi âm...");
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
    } catch (err) {
      console.error("Lỗi khi bắt đầu ghi âm:", err);
    }
  };

  // Dừng ghi âm
  const stopRecording = async () => {
    console.log("Dừng ghi âm...");
    if (!recording) return;

    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    setUri(uri);
    setRecording(null);
    console.log("File đã lưu:", uri);
  };

  // Gửi file âm thanh về server Flask
  const uploadRecording = async () => {
    if (!uri) return;
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", {
        uri,
        name: "recording.m4a",
        type: "audio/m4a",
      } as any);
      // const res = await fetch("http://192.168.43.211:5000/upload", {
      const res = await fetch("http://192.168.1.207:5000/upload", {
      // const res = await fetch ("https://elena-unscrubbed-gyroscopically.ngrok-free.dev/upload", {
        method: "POST",
        body: formData,
        // headers: {
        //   "Content-Type": "multipart/form-data",
        // },
      });

      const data = await res.json();
      console.log("Phản hồi từ server:", data);

      alert(`🤖 ${data.response}`);
    } catch (error) {
      console.error("Lỗi upload:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Button
        title={recording ? "⏹️ Dừng ghi âm" : "🎙️ Bắt đầu ghi âm"}
        onPress={recording ? stopRecording : startRecording}
      />
      {uri && <Text style={styles.text}>📁 File: {uri}</Text>}

      {uri && (
        <Button
          title={uploading ? "⏳ Đang gửi..." : "📤 Gửi file lên server"}
          onPress={uploadRecording}
          disabled={uploading}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  text: { marginVertical: 10 },
});
// import React, { useState } from "react";
// import { View, Button, Text, StyleSheet, Alert } from "react-native";
// import { Audio } from "expo-av";
// import type { Recording } from "expo-av/build/Audio";

// const API_URL = "https://elena-unscrubbed-gyroscopically.ngrok-free.dev";

// export default function App() {
//   const [recording, setRecording] = useState<Recording | null>(null);
//   const [uri, setUri] = useState<string | null>(null);
//   const [uploading, setUploading] = useState(false);

//   const startRecording = async () => {
//     try {
//       await Audio.requestPermissionsAsync();
//       await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });

//       const { recording } = await Audio.Recording.createAsync(
//         Audio.RecordingOptionsPresets.HIGH_QUALITY
//       );

//       setRecording(recording);
//     } catch (err) {
//       console.error("Lỗi khi bắt đầu ghi âm:", err);
//     }
//   };

//   const stopRecording = async () => {
//     if (!recording) return;
//     await recording.stopAndUnloadAsync();
//     const uri = recording.getURI();
//     setUri(uri);
//     setRecording(null);
//   };

//   const uploadRecording = async () => {
//     if (!uri) return;
//     setUploading(true);
//     try {
//       const formData = new FormData();
//       formData.append("file", {
//         uri,
//         name: "recording.m4a",
//         type: "audio/m4a",
//       } as any);

//       const res = await fetch(`${API_URL}/upload`, {
//         method: "POST",
//         body: formData,
//       });

//       const data = await res.json();
//       Alert.alert("Kết quả", `🤖 ${data.response}`);
//     } catch (err) {
//       console.error("Lỗi upload:", err);
//       Alert.alert("Lỗi", "Không thể gửi file. Kiểm tra mạng hoặc ngrok URL.");
//     } finally {
//       setUploading(false);
//     }
//   };

//   return (
//     <View style={styles.container}>
//       <Button
//         title={recording ? "⏹️ Dừng ghi âm" : "🎙️ Bắt đầu ghi âm"}
//         onPress={recording ? stopRecording : startRecording}
//       />
//       {uri && <Text style={styles.text}>📁 File: {uri}</Text>}
//       {uri && (
//         <Button
//           title={uploading ? "⏳ Đang gửi..." : "📤 Gửi file lên server"}
//           onPress={uploadRecording}
//           disabled={uploading}
//         />
//       )}
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: { flex: 1, justifyContent: "center", alignItems: "center" },
//   text: { marginVertical: 10 },
// });
