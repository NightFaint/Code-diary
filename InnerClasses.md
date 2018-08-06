# 内部类

  先来看个例子：
  
    public class TalkingClock
    {
        private int interval;
        private boolean beep;
        public TalkingClock(int interval, boolean beep) { . . . }//构造器
        
        public void start() { . . . }
        
        public class TimePrinter implements ActionListener
        // 一个实现了ActionListener接口的内部类
        {
            public void actionPerformed(ActionEvent event)
            {
                System.out.println("At the tone, the time is " + new Date());
                if (beep) Toolkit.getDefaultToolkit().beep();
            }
        }
    }
    
  之前说过，内部类能访问外部类对象的实例域beep，而内部类TimePrinter本身没有实例域或名为beep的变量。实际上，
  内部类的对象总有一个隐式引用，它指向了创建它的外部类对象，如图：
  
  ![内部类隐式引用](/img/内部类隐式引用.png)
  
  假设将外围类对象的引用称为outer。则actionPerformed方法中if(beep)相当于if(outer.beep)。
  
  外围类的引用是在构造器中设置的。编译器修改了所以内部类的构造器，使得它们添加了外围类的引用参数。由于TimePrinter没有定义构造器，
  所以编译器为这个类生成了一个默认的构造器，代码如下：
  
    public TimePrinter(TalkingClock clock) // automatically generated code
    {
        outer = clock;
    }
  
  注意，outer不是Java关键字，这里仅作说明之用。
  
  当在start方法中创建TimePrinter对象，编译器就会将this引用传递给当前的TimePrinter构造器。
  
  相当于:
  
    ActionListener listener = new TimePrinter(this); // this参数会自动添加
  
  完整代码：
    
    //innerClass//InnerClassTest.java
    package innerClass;

    import java.awt.*;
    import java.awt.event.*;
    import java.util.*;
    import javax.swing.*;
    import javax.swing.Timer;
    /**
    * This program demonstrates the use of inner classes.
    * @version 1.11 2015-05-12
    * @author Cay Horstmann
    */
    public class InnerClassTest
    {
        public static void main(String[] args)
        {
            TalkingClock clock = new TalkingClock(1000, true);
            clock.start();
            
            // keep program running until user selects "Ok"
            JOptionPane.showMessageDialog(null, "Quit program?");
            System.exit(0);
        }
    }
    /**
    * A clock that prints the time in regular intervals.
    */
    
    class TalkingClock
    {
        private int interval;
        private boolean beep;
        /**
        * Constructs a talking clock
        * @param interval the interval between messages (in milliseconds)
        * @param beep true if the clock should beep
        */
        
        public TalkingClock(int interval, boolean beep)
        {
            this.interval = interval;
            this.beep = beep;
        }
        /**
        * Starts the clock.
        */
        public void start()
        {
            ActionListener listener = new TimePrinter();
            Timer t = new Timer(interval, listener);
            t.start();
        }
        
        public class TimePrinter implements ActionListener
        {
            public void actionPerformed(ActionEvent event)
            {
                System.out.println("At the tone, the time is " + new Date());
                if (beep) Toolkit.getDefaultToolkit().beep();
            }
        }
    }

    
  
