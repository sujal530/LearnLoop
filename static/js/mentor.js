document.addEventListener("DOMContentLoaded", function () {
  const chatLog = document.getElementById("mentor-chat-log");
  const mentorForm = document.getElementById("mentor-form");
  const mentorInput = document.getElementById("mentor-input");

  // Auto-scroll chat to the bottom on page load
  function scrollToBottom() {
    if (chatLog) {
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  }

  scrollToBottom();

  // Focus input field automatically
  if (mentorInput) {
    mentorInput.focus();
  }
});