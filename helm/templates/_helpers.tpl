# Application server image
{{- define "helm.server" }}
{{- if .Values.server.tag  }}
- name: "{{ .Release.Name }}"
  image: {{ .Values.server.repository }}:{{ .Values.server.tag }}
{{- else }}
- name: "{{ .Release.Name }}"
  image: {{ .Values.server.repository }}
{{- end }}
{{- end  }}

# Application database
{{- define "helm.database" }}
- name: "{{ .Release.Name }}"
  {{- if .Values.database.tag  }}
  image: {{ .Values.database.repository }}:{{ .Values.database.tag }}
  {{- else }}
  image: {{ .Values.database.repository }}
  {{- end }}
{{- end  }}