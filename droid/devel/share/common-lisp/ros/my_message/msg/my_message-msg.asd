
(cl:in-package :asdf)

(defsystem "my_message-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "my_message" :depends-on ("_package_my_message"))
    (:file "_package_my_message" :depends-on ("_package"))
  ))