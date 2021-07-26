;; Auto-generated. Do not edit!


(when (boundp 'my_message::my_message)
  (if (not (find-package "MY_MESSAGE"))
    (make-package "MY_MESSAGE"))
  (shadow 'my_message (find-package "MY_MESSAGE")))
(unless (find-package "MY_MESSAGE::MY_MESSAGE")
  (make-package "MY_MESSAGE::MY_MESSAGE"))

(in-package "ROS")
;;//! \htmlinclude my_message.msg.html


(defclass my_message::my_message
  :super ros::object
  :slots (_some_floats ))

(defmethod my_message::my_message
  (:init
   (&key
    ((:some_floats __some_floats) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _some_floats __some_floats)
   self)
  (:some_floats
   (&optional __some_floats)
   (if __some_floats (setq _some_floats __some_floats)) _some_floats)
  (:serialization-length
   ()
   (+
    ;; float64[] _some_floats
    (* 8    (length _some_floats)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _some_floats
     (write-long (length _some_floats) s)
     (dotimes (i (length _some_floats))
       (sys::poke (elt _some_floats i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _some_floats
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _some_floats (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _some_floats i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get my_message::my_message :md5sum-) "97ab95377be0b99d91d817753c93dd06")
(setf (get my_message::my_message :datatype-) "my_message/my_message")
(setf (get my_message::my_message :definition-)
      "float64[] some_floats
")



(provide :my_message/my_message "97ab95377be0b99d91d817753c93dd06")


